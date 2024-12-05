export type CustomMetaData = {
    crs: string, 
    data_type: string,
    description: string,
    format: string,
    file_name: string
}

export type FileMetaData = {
    driver: string,
    dtype: string,
    nodata: number,
    width: number,
    height: number,
    count: number,
    crs: string,
    transform: Array<number>
}