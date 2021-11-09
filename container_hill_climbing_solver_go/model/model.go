package model

type MiddleProxyRequest struct {
	BoardArray [][]uint8 `json:"board_array"`
	ZoneLength uint16    `json:"zone_length"`
	ZoneHeight uint16    `json:"zone_height"`
	Restarts   uint16    `json:"restarts"`
	Searchs    uint16    `json:"searchs"`
}

type BoardFitnessReportRequest struct {
	ZoneLength uint16    `json:"zone_length"`
	ZoneHeight uint16    `json:"zone_height"`
	BoardArray [][]uint8 `json:"board"`
}

type BoardFitnessReportResponse struct {
	TotalCollisions  uint16 `json:"total_collisions"`
	ColumnCollisions uint16 `json:"column_collisions"`
	RowCollisions    uint16 `json:"row_collisions"`
	ZoneCollisions   uint16 `json:"zone_collisions"`
}

type BoardFitnessSingleRequest struct {
	ZoneLength uint16    `json:"zone_length"`
	ZoneHeight uint16    `json:"zone_height"`
	BoardArray [][]uint8 `json:"board"`
}

type BoardFitnessSingleResponse struct {
	FitnessScore uint16 `json:"fitness_score"`
}
