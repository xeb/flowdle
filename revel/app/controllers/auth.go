package controllers

import "github.com/robfig/revel"

type Auth struct {
	*revel.Controller
}

func (c Auth) Index() revel.Result {
	return c.Render()
}
