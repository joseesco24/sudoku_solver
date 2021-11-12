package main

type Genome struct {
	Board [][]uint8
	Score uint16
}

type MiddleProxyRequest struct {
	InitialBoard [][]uint8 `json:"initial_board"`
	ZoneLength   uint16    `json:"zone_length"`
	ZoneHeight   uint16    `json:"zone_height"`
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
	ZoneLength uint16    `json:"zoneLength"`
	ZoneHeight uint16    `json:"zoneHeight"`
	BoardArray [][]uint8 `json:"board"`
}

type BoardFitnessReportResponse struct {
	ColumnCollisions uint16 `json:"columnCollisions"`
	TotalCollisions  uint16 `json:"totalCollisions"`
	ZoneCollisions   uint16 `json:"zoneCollisions"`
	RowCollisions    uint16 `json:"rowCollisions"`
}

type BoardFitnessSingleRequest struct {
	ZoneLength uint16    `json:"zoneLength"`
	ZoneHeight uint16    `json:"zoneHeight"`
	BoardArray [][]uint8 `json:"board"`
}

type BoardFitnessSingleResponse struct {
	FitnessScore uint16 `json:"fitnessScore"`
}

type BoardRandomInitializationRequest struct {
	FixedNumbersBoard [][]uint8 `json:"fixedNumbersBoard"`
	ZoneLength        uint16    `json:"zoneLength"`
	ZoneHeight        uint16    `json:"zoneHeight"`
}

type BoardRandomInitializationResponse struct {
	Board [][]uint8 `json:"board"`
}

type BoardRandomMutationRequest struct {
	FixedNumbersBoard [][]uint8 `json:"fixedNumbersBoard"`
	BoardArray        [][]uint8 `json:"board"`
}

type BoardRandomMutationResponse struct {
	Board [][]uint8 `json:"board"`
}
