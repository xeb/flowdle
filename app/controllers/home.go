package controllers

import (
	"fmt"
	"github.com/revel/revel"
	"github.com/xeb/flowdle/app/services"
)

type Home struct {
	*revel.Controller
}

func (c Home) Index() revel.Result {

	userid := c.Session["userid"]
	if userid != "" {
		bucket := services.GetBucket()
		r, err := bucket.GetRaw(fmt.Sprintf("authtoken-%s", userid))
		if err == nil && len(r) > 0 {
			return c.Redirect("/tasks")
		}
	}

	return c.Render()
}
