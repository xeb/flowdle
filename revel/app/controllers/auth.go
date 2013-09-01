package controllers

import (
	"flowdle/app/services"
	"fmt"
	"github.com/robfig/revel"
)

type Auth struct {
	*revel.Controller
}

func (c Auth) Index() revel.Result {

	r, _ := services.TryOAuth()

	if r.Success == false {
		return c.Redirect(r.AuthURL)
	}

	return c.Render()
}

func (c Auth) Callback() revel.Result {

	r, _ := services.TryOAuth()

	if r.Success {
		return c.RenderText(fmt.Sprintf("It worked! %s", r))
	}

	return c.RenderText("Not quite")
}
