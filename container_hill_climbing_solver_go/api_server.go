package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func main() {

	e := echo.New()

	e.GET("/health_test", func(context echo.Context) error {

		return context.NoContent(http.StatusOK)

	})

	e.GET("/solver", func(context echo.Context) error {

		return context.NoContent(http.StatusOK)

	})

	e.Start(":3000")

}
