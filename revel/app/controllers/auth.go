package controllers

import (
	"flowdle/app/services"
	"fmt"
	"github.com/robfig/revel"
)

type Auth struct {
	*revel.Controller
}

var (
	bucket = services.GetBucket()
)

func (c Auth) Index() revel.Result {
	tokenCache := services.NewOAuthCache(c.Session, bucket)
	r, _ := services.TryOAuth(*tokenCache, "")

	if r.Success == false {
		return c.Redirect(r.AuthURL)
	}

	return c.RenderText(fmt.Sprintf("Already logged in! %s", r))
}

func (c Auth) Callback() revel.Result {
	tokenCache := services.NewOAuthCache(c.Session, bucket)
	code := c.Params.Get("code")
	r, _ := services.TryOAuth(tokenCache, code)

	if r.Success {
		return c.RenderText(fmt.Sprintf("It worked! %s", r))
	}

	return c.RenderText("Not quite")
}
