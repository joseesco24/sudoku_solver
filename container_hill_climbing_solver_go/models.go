package main

type MiddleProxyRequest struct {
	InitialBoard [][]uint8 `json:"initialBoard"`
	ZoneLength   uint16    `json:"zoneLength"`
	ZoneHeight   uint16    `json:"zoneHeight"`
	Restarts     uint16    `json:"restarts"`
	Searchs      uint16    `json:"searchs"`
}

type MiddleProxyResponse struct {
	ColumnCollisions uint16    `json:"columnCollisions"`
	TotalCollisions  uint16    `json:"totalCollisions"`
	ZoneCollisions   uint16    `json:"zoneCollisions"`
	RowCollisions    uint16    `json:"rowCollisions"`
	SolutionBoard    [][]uint8 `json:"solutionBoard"`
}

type BoardFitnessReportRequest struct {
	ZoneLength uint16    `json:"zone_length"`
	ZoneHeight uint16    `json:"zone_height"`
	BoardArray [][]uint8 `json:"board"`
}

type BoardFitnessReportResponse struct {
	ColumnCollisions uint16 `json:"column_collisions"`
	TotalCollisions  uint16 `json:"total_collisions"`
	ZoneCollisions   uint16 `json:"zone_collisions"`
	RowCollisions    uint16 `json:"row_collisions"`
}

type BoardFitnessSingleRequest struct {
	ZoneLength uint16    `json:"zone_length"`
	ZoneHeight uint16    `json:"zone_height"`
	BoardArray [][]uint8 `json:"board"`
}

type BoardFitnessSingleResponse struct {
	FitnessScore uint16 `json:"fitness_score"`
}

type BoardRandomInitializationRequest struct {
	FixedNumbersBoard [][]uint8 `json:"fixed_numbers_board"`
	ZoneLength        uint16    `json:"zone_length"`
	ZoneHeight        uint16    `json:"zone_height"`
}

type BoardRandomInitializationResponse struct {
	Board [][]uint8 `json:"board"`
}

type BoardRandomMutationRequest struct {
	FixedNumbersBoard [][]uint8 `json:"fixed_numbers_board"`
	BoardArray        [][]uint8 `json:"board"`
}

type BoardRandomMutationResponse struct {
	Board [][]uint8 `json:"board"`
}
