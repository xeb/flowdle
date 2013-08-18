package controllers

import "github.com/robfig/revel"

type Home struct {
	*revel.Controller
}

func (c Home) Index() revel.Result {
	return c.Render()
}
