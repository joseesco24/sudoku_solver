package main

import (
	"encoding/json"
	"net/http"
	"os"

	"github.com/ansel1/merry"
	"github.com/go-resty/resty/v2"
)

var apiKey string = os.Getenv("SOLVER_FUNCTIONS_KEY")

/*
   This function uses the general solver functions api to calculate and return all the different collisions on a given board array
   representation.
*/
func CalculateBoardFitnessReport(board [][]uint8, zoneHeight, zoneLength uint16) (totalCollisions, columnCollisions, rowCollisions, zoneCollisions uint16, err error) {

	var boardFitnessReportApiUrl string = os.Getenv("FITNESS_REPORT_SCORE_LINK")
	boardFitnessReportRequest := &BoardFitnessReportRequest{
		ZoneHeight: zoneHeight,
		ZoneLength: zoneLength,
		BoardArray: board,
	}

	boardFitnessReportResponse, err := resty.New().R().
		SetHeader("Content-Type", "application/json").
		SetHeader("Authorization", apiKey).
		SetBody(boardFitnessReportRequest).
		Get(boardFitnessReportApiUrl)

	if err != nil {
		return 0, 0, 0, 0, merry.Wrap(err).Append("unable to get the board fitness report").
			WithValue("response code", boardFitnessReportResponse.Status()).
			WithValue("request body", boardFitnessReportRequest).
			WithHTTPCode(http.StatusInternalServerError)
	}

	if !boardFitnessReportResponse.IsSuccess() {
		return 0, 0, 0, 0, merry.New("error while getting the board fitness report").
			WithValue("response code", boardFitnessReportResponse.Status()).
			WithValue("request body", boardFitnessReportRequest).
			WithHTTPCode(http.StatusInternalServerError)
	}

	var boardFitnessReportResponseRawBody []byte = boardFitnessReportResponse.Body()
	var boardFitnessReportResponseBody BoardFitnessReportResponse

	err = json.Unmarshal(boardFitnessReportResponseRawBody, &boardFitnessReportResponseBody)
	if err != nil {
		return 0, 0, 0, 0, merry.New("error while unmarshalling the board fitness response body").
			WithValue("response body", string(boardFitnessReportResponseRawBody)).
			WithHTTPCode(http.StatusInternalServerError)
	}

	return boardFitnessReportResponseBody.TotalCollisions,
		boardFitnessReportResponseBody.ColumnCollisions,
		boardFitnessReportResponseBody.RowCollisions,
		boardFitnessReportResponseBody.ZoneCollisions,
		nil

}

/*
   This function uses the general solver functions api to calculate and return the total of all the collisions on a given board
   array representation.
*/
func CalculateBoardFitnessSingle(board [][]uint8, zoneHeight, zoneLength uint16) (fitnessScore uint16, err error) {

	var boardFitnessSingleApiUrl string = os.Getenv("FITNESS_SINGLE_SCORE_LINK")
	boardFitnessReportRequest := &BoardFitnessSingleRequest{
		ZoneHeight: zoneHeight,
		ZoneLength: zoneLength,
		BoardArray: board,
	}

	boardFitnessSingleResponse, err := resty.New().R().
		SetHeader("Content-Type", "application/json").
		SetHeader("Authorization", apiKey).
		SetBody(boardFitnessReportRequest).
		Get(boardFitnessSingleApiUrl)

	if err != nil {
		return 0, merry.Wrap(err).Append("unable to get the board fitness score").
			WithValue("response code", boardFitnessSingleResponse.Status()).
			WithValue("request body", boardFitnessReportRequest).
			WithHTTPCode(http.StatusInternalServerError)
	}

	if !boardFitnessSingleResponse.IsSuccess() {
		return 0, merry.New("error while getting the board fitness score").
			WithValue("response code", boardFitnessSingleResponse.Status()).
			WithValue("request body", boardFitnessReportRequest).
			WithHTTPCode(http.StatusInternalServerError)
	}

	var boardFitnessSingleResponseRawBody []byte = boardFitnessSingleResponse.Body()
	var boardFitnessSingleResponseBody BoardFitnessSingleResponse

	err = json.Unmarshal(boardFitnessSingleResponseRawBody, &boardFitnessSingleResponseBody)
	if err != nil {
		return 0, merry.New("error while unmarshalling the board fitness response body").
			WithValue("response body", string(boardFitnessSingleResponseRawBody)).
			WithHTTPCode(http.StatusInternalServerError)
	}

	return boardFitnessSingleResponseBody.FitnessScore, nil

}
