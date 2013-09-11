package services

import (
	"bufio"
	"bytes"
	"code.google.com/p/goauth2/oauth"
	"encoding/json"
	"log"
	"os"
	"fmt"
	"strings"
)

var (
	scope       = "https://www.googleapis.com/auth/userinfo.profile"
	redirectURL = "http://localhost:9000/oauth2callback"
	authURL     = "https://accounts.google.com/o/oauth2/auth"
	tokenURL    = "https://accounts.google.com/o/oauth2/token"
	requestURL  = "https://www.googleapis.com/oauth2/v1/userinfo"
	nixRoot 	= "/etc/flowdle/"
	winRoot		= "c:\\cygwin64\\etc\\flowdle\\"
	clientId, _ = readFlowdleConfig("clientid")
	secret, _   = readFlowdleConfig("secret")
)

type OAuthResult struct {
	Success bool
	AuthURL string
	Account *Account
	Token   *oauth.Token
}

type Account struct {
	Id      string `json:"id"`
	Name    string `json:"name"`
	Picture string `json:"picture"`
}

func parseAccount(data string) (acc *Account, err error) {
	acc = &Account{}
	dec := json.NewDecoder(strings.NewReader(data))
	if err = dec.Decode(acc); err != nil {
		return nil, err
	}
	return acc, nil
}

func readFlowdleConfig(fileName string) (string, error) {
	path := nixRoot
	exists, _ := exists(path)
	if exists == false {
		path = winRoot
	}
	
	fullPath := fmt.Sprintf("%s%s", path, fileName)

	file, err := os.Open(fullPath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	return scanner.Text(), scanner.Err()
}

func exists(path string) (bool, error) {
    _, err := os.Stat(path)
    if err == nil { return true, nil }
    if os.IsNotExist(err) { return false, nil }
    return false, err
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
	result.Success = true
	result.Token = token
	result.Account, err = parseAccount(s)
	if err != nil {
		log.Fatal("parseAccount:", err)
		e = err
	}

	return
}
