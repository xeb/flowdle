package services

import (
	"code.google.com/p/goauth2/oauth"
	"errors"
	"fmt"
	"github.com/couchbaselabs/go-couchbase"
	"github.com/revel/revel"
)

type OAuthCache struct {
	session revel.Session
	bucket  *couchbase.Bucket
}

func NewOAuthCache(s revel.Session, b *couchbase.Bucket) *OAuthCache {
	oauthcache := &OAuthCache{session: s, bucket: b}
	return oauthcache
}

func (c OAuthCache) Token() (*oauth.Token, error) {
	var tok oauth.Token
	c.bucket.Get(fmt.Sprintf("authtoken-%s", c.session["authtoken"]), &tok)
	if tok.Expired() || tok.AccessToken == "" {
		return nil, errors.New("No AccessToken available")
	}
	return &tok, nil
}

func (c OAuthCache) PutToken(tok *oauth.Token) error {
	c.bucket.Set(fmt.Sprintf("authtoken-%s", tok.AccessToken), int(tok.Expiry.Unix()), tok)
	c.session["authtoken"] = tok.AccessToken
	return nil
}
