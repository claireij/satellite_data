export type Bounds = [[number, number], [number, number]];

export type CustomMetaData = {
    crs: string, 
    data_type: string,
    description: string,
    format: string,
    file_name: string
    bounds: Bounds
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