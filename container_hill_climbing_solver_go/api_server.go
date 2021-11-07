package main

import (
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/labstack/echo/v4"
)

func main() {

	e := echo.New()

	e.POST("/webhooks/gupshup/events/:destinationPhoneNumberCode/:destinationPhoneNumber", func(context echo.Context) error {

		defer func(context echo.Context) {

			body, _ := ioutil.ReadAll(context.Request().Body)

			fmt.Println()
			fmt.Println(string(body))
			fmt.Println()

		}(context)

		return context.NoContent(http.StatusOK)

	})

	e.Start(":3000")

}
