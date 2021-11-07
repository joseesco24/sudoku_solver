package model

type Request struct {
	BoardArray [][]uint8 `json:"board_array"`
	ZoneLength uint16    `json:"zone_length"`
	ZoneHeight uint16    `json:"zone_height"`
	Restarts   uint16    `json:"restarts"`
	Searchs    uint16    `json:"searchs"`
}
