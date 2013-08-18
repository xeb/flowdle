package controllers

import "github.com/robfig/revel"

type Tasks struct {
	*revel.Controller
}

func (c Tasks) Index() revel.Result {
	return c.Render()
}
