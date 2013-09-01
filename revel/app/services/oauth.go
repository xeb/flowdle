package services

import (
	"bufio"
	"bytes"
	"code.google.com/p/goauth2/oauth"
	"log"
	"os"
)

var (
	scope       = "https://www.googleapis.com/auth/userinfo.profile"
	redirectURL = "http://localhost:9000/oauth2callback"
	authURL     = "https://accounts.google.com/o/oauth2/auth"
	tokenURL    = "https://accounts.google.com/o/oauth2/token"
	requestURL  = "https://www.googleapis.com/oauth2/v1/userinfo"
	clientId, _ = readLine("/etc/flowdle/clientid")
	secret, _   = readLine("/etc/flowdle/secret")
)

type OAuthResult struct {
	Success bool
	AuthURL string
	Debug   string
	Token   *oauth.Token
}

func readLine(path string) (string, error) {
	file, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	return scanner.Text(), scanner.Err()
}

func TryOAuth(cache oauth.Cache, code string) (result *OAuthResult, e error) {
	result = &OAuthResult{}

	config := &oauth.Config{
		ClientId:     clientId,
		ClientSecret: secret,
		RedirectURL:  redirectURL,
		Scope:        scope,
		AuthURL:      authURL,
		TokenURL:     tokenURL,
		TokenCache:   cache,
	}

	transport := &oauth.Transport{Config: config}

	// Try to pull the token from the cache; if this fails, we need to get one.
	token, err := config.TokenCache.Token()
	if err != nil {
		if clientId == "" {
			panic("Cannot find clientId.  Check /etc/flowdle")
			return
		}
		if secret == "" {
			panic("Cannot find secret.  Check /etc/flowdle")
			return
		}
		if code == "" {
			url := config.AuthCodeURL("")
			result.Success = false
			result.AuthURL = url
			return
		}

		token, err = transport.Exchange(code)
		if err != nil {
			log.Fatal("Exchange:", err)
			e = err
		}
	}

	transport.Token = token

	r, err := transport.Client().Get(requestURL)
	if err != nil {
		log.Fatal("Get:", err)
		e = err
	}
	defer r.Body.Close()

	buf := new(bytes.Buffer)
	buf.ReadFrom(r.Body)
	s := buf.String()
	result.Debug = s
	result.Success = true
	result.Token = token

	// log.Printf("Result success %s", result)

	return
}
