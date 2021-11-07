package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/ansel1/merry"
	"github.com/labstack/echo/v4"
)

func main() {

	e := echo.New()

	e.GET("/health_test", func(context echo.Context) error {

		return context.NoContent(http.StatusOK)

	})

	e.GET("/solver", func(context echo.Context) error {

		var authorization string = context.Request().Header.Get("Authorization")

		if authorization == "" {
			return merry.New("authorization not found").
				WithValue("authorization", authorization).
				WithUserMessage("authorization not found").
				WithHTTPCode(http.StatusUnauthorized)
		}

		if authorization != os.Getenv("ACCESS_KEY") {
			return merry.New("authorization not valid").
				WithValue("authorization", authorization).
				WithUserMessage("authorization not valid").
				WithHTTPCode(http.StatusUnauthorized)
		}

		return context.NoContent(http.StatusOK)

	})

	e.Start(fmt.Sprintf(":%s", os.Getenv("ACCESS_PORT")))

}
