from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from pathlib import Path
import uuid

from app.services.data_profiler import profile_dataset
from app.services.dataset_storage import load_dataset, save_dataset


router = APIRouter(
   prefix="/api/datasets",
    tags=["Datasets"]
)


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

        await save_dataset(dataset_id, extension, contents)

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
async def get_dataset_profile(dataset_id: str):
    stored_dataset = await load_dataset(dataset_id)

    if stored_dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    extension, contents = stored_dataset

    try:
        if extension == ".csv":
            dataframe = pd.read_csv(BytesIO(contents))
        else:
            dataframe = pd.read_excel(BytesIO(contents))

        profile = profile_dataset(dataframe)

        return {
            "dataset_id": dataset_id,
            "filename": f"{dataset_id}{extension}",
            "profile": profile
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Error reading dataset: {str(error)}"
        )