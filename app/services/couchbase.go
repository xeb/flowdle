package services

import (
	"fmt"
	"github.com/couchbaselabs/go-couchbase"
	"log"
)

var (
	bucket *couchbase.Bucket
	server = ReadConfigOrDefault("server", "http://localhost:8091/")
)

func GetBucket() (b *couchbase.Bucket) {

	if bucket != nil {
		return bucket
	}

	fmt.Printf("COUCHBASE Connecting to %s\n", server)

	b, err := couchbase.GetBucket(server, "default", "flowdle")
	if err != nil {
		log.Fatal("Cannot connect %s", err)
	}

	bucket = b
	return b
}
