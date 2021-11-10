package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"

	"github.com/ansel1/merry"
	"github.com/labstack/echo/v4"
)

func main() {

	e := echo.New()

	/*
		This function is incharge of response all the health check petitions that the middle proxy makes for checking if the requested
		solver is active before making a solver request.
	*/
	e.GET("/health_test", func(context echo.Context) error {

		return context.NoContent(http.StatusOK)

	})

	/*
		This function is in charge to expose the solver functionality, this function receives the board solve parameters and initial
		board in the body of a json http request and returns response with the board best solution that this solver could find using
		the hill climbing algorithm in the response body also using json format.
	*/
	e.GET("/solver", func(context echo.Context) error {

		var authorization string = context.Request().Header.Get("Authorization")

		if authorization == "" {
			return merry.New("authorization not found").
				WithValue("middleProxyAuthorization", authorization).
				WithUserMessage("authorization not found").
				WithHTTPCode(http.StatusUnauthorized)
		}

		if authorization != os.Getenv("ACCESS_KEY") {
			return merry.New("authorization not valid").
				WithValue("middleProxyAuthorization", authorization).
				WithUserMessage("authorization not valid").
				WithHTTPCode(http.StatusUnauthorized)
		}

		var middleProxyRequestBody MiddleProxyRequest

		body, err := ioutil.ReadAll(context.Request().Body)
		if err != nil {
			return merry.Wrap(err).Append("error while loading the middle proxy request body").
				WithValue("middleProxyRequestBody", string(body)).
				WithHTTPCode(http.StatusInternalServerError)
		}

		err = json.Unmarshal(body, &middleProxyRequestBody)
		if err != nil {
			return merry.Wrap(err).Append("error while unmarshalling the middle proxy request body").
				WithValue("middleProxyRequestBody", string(body)).
				WithHTTPCode(http.StatusInternalServerError)
		}

		if middleProxyRequestBody.Restarts == 0 {
			middleProxyRequestBody.Restarts = 10
		}

		if middleProxyRequestBody.Searchs == 0 {
			middleProxyRequestBody.Searchs = 10
		}

		return context.NoContent(http.StatusOK)

	})

	e.Start(fmt.Sprintf(":%s", os.Getenv("ACCESS_PORT")))

}
