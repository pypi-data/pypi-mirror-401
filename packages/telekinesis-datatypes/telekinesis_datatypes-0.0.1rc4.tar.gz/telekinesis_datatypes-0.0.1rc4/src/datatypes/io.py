import pathlib
import numpy as np
from typing import Optional, Sequence
from loguru import logger
from plyfile import PlyData, PlyElement
import trimesh
import cv2

from datatypes import datatypes


# ============================================================
# POINT CLOUD LOADING
# ============================================================

def load_point_cloud(
    filepath: str,
    remove_nan_points: bool = True,
    remove_infinite_points: bool = True,
    remove_duplicated_points: bool = True,
) -> Optional[datatypes.Points3D]:
    """
    Load a PLY point cloud into Points3D.
    """

    path = pathlib.Path(filepath)
    if not path.is_file():
        logger.error(f"Point cloud file does not exist: {filepath}")
        return None

    ply = PlyData.read(str(path))
    if "vertex" not in ply:
        logger.error("PLY file has no vertex element")
        return None

    v = ply["vertex"]

    positions = np.column_stack((v["x"], v["y"], v["z"])).astype(np.float32)

    normals = None
    if all(k in v for k in ("nx", "ny", "nz")):
        normals = np.column_stack((v["nx"], v["ny"], v["nz"])).astype(np.float32)

    colors = None
    if all(k in v for k in ("red", "green", "blue")):
        r = v["red"].astype(np.uint32)
        g = v["green"].astype(np.uint32)
        b = v["blue"].astype(np.uint32)
        a = v["alpha"].astype(np.uint32) if "alpha" in v else np.full_like(r, 255)
        colors = ((r << 24) | (g << 16) | (b << 8) | a).astype(np.uint32)

    # -------- filtering --------
    mask = np.ones(len(positions), dtype=bool)

    if remove_nan_points or remove_infinite_points:
        mask &= np.isfinite(positions).all(axis=1)

    positions = positions[mask]
    if normals is not None:
        normals = normals[mask]
    if colors is not None:
        colors = colors[mask]

    if remove_duplicated_points and len(positions) > 0:
        unique_pos, idx = np.unique(positions, axis=0, return_index=True)
        positions = unique_pos
        if normals is not None:
            normals = normals[idx]
        if colors is not None:
            colors = colors[idx]

    if len(positions) == 0:
        logger.error("Loaded point cloud is empty after filtering")
        return None

    return datatypes.Points3D(
        positions=positions,
        normals=normals,
        colors=colors,
    )


# ============================================================
# POINT CLOUD WRITING
# ============================================================

def save_point_cloud(
    point_clouds: Sequence[datatypes.Points3D],
    filepath: str,
) -> bool:
    """
    Save one or more Points3D objects to a PLY file.
    """

    if not point_clouds:
        logger.error("No point clouds provided for writing")
        return False

    positions = np.vstack([pc.positions for pc in point_clouds])

    colors = None
    if any(pc.colors is not None for pc in point_clouds):
        color_blocks = []
        for pc in point_clouds:
            if pc.colors is not None:
                color_blocks.append(pc.colors)
            else:
                color_blocks.append(
                    np.full(len(pc.positions), 0xFFFFFFFF, dtype=np.uint32)
                )
        colors = np.concatenate(color_blocks)

    dtype = [("x", "f4"), ("y", "f4"), ("z", "f4")]
    data = {
        "x": positions[:, 0],
        "y": positions[:, 1],
        "z": positions[:, 2],
    }

    if colors is not None:
        dtype += [("red", "u1"), ("green", "u1"), ("blue", "u1"), ("alpha", "u1")]
        data["red"]   = (colors >> 24) & 0xFF
        data["green"] = (colors >> 16) & 0xFF
        data["blue"]  = (colors >> 8) & 0xFF
        data["alpha"] = colors & 0xFF

    arr = np.empty(len(positions), dtype=dtype)
    for k, v in data.items():
        arr[k] = v

    path = pathlib.Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    PlyData(
        [PlyElement.describe(arr, "vertex")],
        text=False,
    ).write(str(path))

    return True


# ============================================================
# MESH LOADING
# ============================================================

def load_mesh(
    filepath: str,
    compute_vertex_normals: bool = False,
    postprocess_mesh: bool = False,
) -> Optional[datatypes.Mesh3D]:
    """
    Load a mesh file into Mesh3D.
    Supports: PLY, OBJ, STL, GLB, GLTF.
    """

    path = pathlib.Path(filepath)
    if not path.is_file():
        logger.error(f"Mesh file does not exist: {filepath}")
        return None

    scene = trimesh.load(str(path), force="scene")

    if isinstance(scene, trimesh.Scene):
        if not scene.geometry:
            logger.error("Mesh file contains no geometry")
            return None
        mesh = trimesh.util.concatenate(tuple(scene.geometry.values()))
    else:
        mesh = scene

    if postprocess_mesh:
        mesh.remove_degenerate_faces()
        mesh.remove_duplicate_faces()
        mesh.remove_unreferenced_vertices()
        mesh.merge_vertices()

    if compute_vertex_normals:
        mesh.rezero()
        _ = mesh.vertex_normals  # force computation

    vertex_colors = None
    if mesh.visual.kind == "vertex":
        vc = mesh.visual.vertex_colors
        if vc is not None:
            vertex_colors = vc[:, :4]

    return datatypes.Mesh3D(
        vertex_positions=mesh.vertices.astype(np.float32),
        triangle_indices=mesh.faces.astype(np.int32),
        vertex_normals=mesh.vertex_normals.astype(np.float32)
        if mesh.vertex_normals is not None else None,
        vertex_colors=vertex_colors,
    )


# ============================================================
# MESH WRITING
# ============================================================

def save_mesh(
    mesh: datatypes.Mesh3D,
    filepath: str,
) -> bool:
    """
    Save Mesh3D to PLY / GLB / GLTF / STL / OBJ (based on extension).
    """

    trimesh_mesh = trimesh.Trimesh(
        vertices=mesh.vertex_positions,
        faces=mesh.triangle_indices,
        vertex_normals=mesh.vertex_normals,
        process=False,
    )

    if mesh.vertex_colors is not None:
        rgba = mesh.vertex_colors.astype(np.uint32)
        colors = np.column_stack([
            (rgba >> 24) & 0xFF,
            (rgba >> 16) & 0xFF,
            (rgba >> 8)  & 0xFF,
            rgba & 0xFF,
        ]).astype(np.uint8)
        trimesh_mesh.visual.vertex_colors = colors

    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    trimesh_mesh.export(filepath)

    return True


# ============================================================
# IMAGE LOADING
# ============================================================

def load_image(
    filepath: str,
    *,
    color_model: Optional["datatypes.ColorModelLike"] = None,
    keep_alpha: bool = True,
    as_gray: bool = False,

    # --- New: binary mask output ---
    as_binary: bool = False,
    binary_method: str = "otsu",      # "otsu" | "fixed" | "adaptive"
    binary_threshold: int = 127,      # used when binary_method == "fixed"
    adaptive_block_size: int = 31,    # used when binary_method == "adaptive" (must be odd)
    adaptive_C: int = 2,              # used when binary_method == "adaptive"
    invert: bool = False,             # if True, invert foreground/background
) -> Optional[datatypes.Image]:
    """
    Load an image file into datatypes.Image.

    Args:
        filepath:
            Path to the image file (png/jpg/...).
        color_model:
            Optional explicit color model. If None, it will be inferred by datatypes.Image(...).
        keep_alpha:
            If True, preserve alpha channel when present (cv2.IMREAD_UNCHANGED).
        as_gray:
            If True, force grayscale output (single channel).

        as_binary (NEW):
            If True, return a single-channel binary mask image with dtype uint8 and values {0, 255}.
            Note: When as_binary=True, the image is read in grayscale mode internally.
        binary_method (NEW):
            Binarization method:
              - "otsu" (default): Otsu thresholding (automatic threshold).
              - "fixed": fixed threshold using `binary_threshold`.
              - "adaptive": adaptive thresholding using `adaptive_block_size` and `adaptive_C`.
        binary_threshold (NEW):
            Fixed threshold value used when binary_method == "fixed".
        adaptive_block_size (NEW):
            Block size for adaptive thresholding (must be odd and >= 3).
        adaptive_C (NEW):
            Constant subtracted from the mean/weighted mean in adaptive thresholding.
        invert (NEW):
            If True, invert the binary result (swap foreground/background).

    Returns:
        datatypes.Image or None if loading failed.
    """
    path = pathlib.Path(filepath)
    if not path.is_file():
        logger.error(f"Image file does not exist: {filepath}")
        return None

    # Decide OpenCV read flag:
    # - For binary output we must start from grayscale (single channel).
    # - Otherwise keep the original behavior (unchanged / color).
    if as_gray or as_binary:
        flag = cv2.IMREAD_GRAYSCALE
    else:
        flag = cv2.IMREAD_UNCHANGED if keep_alpha else cv2.IMREAD_COLOR

    img = cv2.imread(str(path), flag)
    if img is None:
        logger.error(f"Failed to read image: {filepath}")
        return None

    # OpenCV returns:
    # - grayscale: (H, W)
    # - color: (H, W, 3) BGR
    # - with alpha: (H, W, 4) BGRA
    #
    # If NOT grayscale and NOT binary, convert OpenCV's BGR/BGRA to RGB/RGBA.
    if (not as_gray) and (not as_binary) and img.ndim == 3:
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

    # --- NEW: optional binarization path ---
    if as_binary:
        # `img` should already be grayscale due to IMREAD_GRAYSCALE.
        # This is a safety fallback in case something upstream changes.
        if img.ndim == 3:
            if img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            else:
                raise RuntimeError(
                    f"Unsupported channel count for binary conversion: {img.shape[2]}"
                )

        method = (binary_method or "otsu").lower()

        if method == "fixed":
            # Fixed threshold: pixels > threshold become 255 else 0
            thr = int(binary_threshold)
            _, mask = cv2.threshold(img, thr, 255, cv2.THRESH_BINARY)

        elif method == "adaptive":
            # Adaptive threshold requires odd block size >= 3
            bs = int(adaptive_block_size)
            if bs < 3:
                bs = 3
            if bs % 2 == 0:
                bs += 1

            mask = cv2.adaptiveThreshold(
                img,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                bs,
                int(adaptive_C),
            )

        else:
            # Default: Otsu thresholding (automatic threshold selection)
            _, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Optionally invert the mask (foreground <-> background)
        if invert:
            mask = cv2.bitwise_not(mask)

        # Enforce a clean uint8 binary mask with values in {0, 255}
        mask = np.where(mask > 0, 255, 0).astype(np.uint8)
        img = mask

    try:
        return datatypes.Image(image=img, color_model=color_model)
    except Exception as e:
        logger.error(f"Failed to construct datatypes.Image from file '{filepath}': {e}")
        return None


# ============================================================
# IMAGE WRITING
# ============================================================

def save_image(
    images: Sequence[datatypes.Image],
    filepath: str,
    *,
    as_bgr_for_opencv: bool = True,
) -> bool:
    """
    Save one or more datatypes.Image objects to an image file.

    Notes:
    - If multiple images are provided, they will be concatenated horizontally (like a contact sheet).
    - Writes using OpenCV, so image is converted to BGR/BGRA by default.

    Args:
        images: Sequence of datatypes.Image
        filepath: Output path
        as_bgr_for_opencv: Convert RGB/RGBA -> BGR/BGRA before cv2.imwrite

    Returns:
        True on success, False otherwise
    """
    if not images:
        logger.error("No images provided for writing")
        return False

    # Convert to numpy arrays
    np_imgs: list[np.ndarray] = []
    for i, img in enumerate(images):
        if not isinstance(img, datatypes.Image):
            logger.error(f"Item {i} is not a datatypes.Image: {type(img)}")
            return False

        try:
            arr = img.to_numpy()
        except Exception as e:
            logger.error(f"Failed to convert Image[{i}] to numpy: {e}")
            return False

        if not isinstance(arr, np.ndarray):
            logger.error(f"Image[{i}].to_numpy() did not return np.ndarray, got {type(arr)}")
            return False

        # Ensure uint8 for writing
        if arr.dtype != np.uint8:
            if arr.max() <= 1.0:
                arr = (arr * 255).astype(np.uint8)
            else:
                arr = np.clip(arr, 0, 255).astype(np.uint8)

        # Convert RGB/RGBA -> BGR/BGRA if needed for OpenCV writing
        if as_bgr_for_opencv and arr.ndim == 3:
            if arr.shape[2] == 3:
                arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            elif arr.shape[2] == 4:
                arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)

        np_imgs.append(arr)

    # If multiple images: concatenate horizontally
    if len(np_imgs) == 1:
        out = np_imgs[0]
    else:
        # make heights consistent
        heights = [a.shape[0] for a in np_imgs]
        if len(set(heights)) != 1:
            logger.error(f"All images must have same height to concatenate. Heights={heights}")
            return False
        out = np.concatenate(np_imgs, axis=1)

    # Ensure output folder exists
    path = pathlib.Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    ok = cv2.imwrite(str(path), out)
    if not ok:
        logger.error(f"Failed to write image to: {filepath}")
        return False

    return True