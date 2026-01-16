from pydantic import Field, BaseModel

from magdi_data.dataset.nifti_occ_inst_dataset_meta import NiftiOccInstDatasetMeta


class DescriptiveMetaData(BaseModel):
    latin_name: str = Field(default="")
    line_name: str = Field(default="")
    structure: str = Field(default="")
    dap: str = Field(default="")
    device: str = Field(default="")
    coil: str = Field(default="")
    measurement_channel: str = Field(default="")


class PlantNiftiOccInstDatasetMeta(NiftiOccInstDatasetMeta):

    descriptive_metadata: DescriptiveMetaData = Field(
        default_factory=DescriptiveMetaData
    )
