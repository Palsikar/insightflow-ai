from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from pathlib import Path
import uuid

from app.services.data_profiler import profile_dataset


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)


# Folder where uploaded datasets are stored
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    allowed_extensions = [".csv", ".xlsx"]

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    original_filename = file.filename
    filename = original_filename.lower()

    if not filename.endswith(tuple(allowed_extensions)):
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are allowed"
        )

    try:

        # Read uploaded file
        contents = await file.read()

        # Generate unique dataset ID
        dataset_id = str(uuid.uuid4())

        # Get file extension
        extension = Path(original_filename).suffix.lower()

        # Create path for saved dataset
        saved_path = DATA_DIR / f"{dataset_id}{extension}"

        # Save the dataset
        with open(saved_path, "wb") as output_file:
            output_file.write(contents)

        # Read dataset using Pandas
        if extension == ".csv":
            dataframe = pd.read_csv(BytesIO(contents))

        elif extension == ".xlsx":
            dataframe = pd.read_excel(BytesIO(contents))

        # Generate dataset profile
        profile = profile_dataset(dataframe)

        return {
            "message": "Dataset uploaded and profiled successfully",
            "dataset_id": dataset_id,
            "filename": original_filename,
            "profile": profile
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Error processing dataset: {str(error)}"
        )


@router.get("/{dataset_id}/profile")
def get_dataset_profile(dataset_id: str):

    # Find dataset using its ID
    matching_files = list(DATA_DIR.glob(f"{dataset_id}.*"))

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    file_path = matching_files[0]

    try:

        # Read the saved dataset
        if file_path.suffix.lower() == ".csv":
            dataframe = pd.read_csv(file_path)

        elif file_path.suffix.lower() == ".xlsx":
            dataframe = pd.read_excel(file_path)

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        # Generate profile
        profile = profile_dataset(dataframe)

        return {
            "dataset_id": dataset_id,
            "filename": file_path.name,
            "profile": profile
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Error reading dataset: {str(error)}"
        )