package services

import (
	"github.com/couchbaselabs/go-couchbase"
	"log"
)

var bucket *couchbase.Bucket

func GetBucket() (b *couchbase.Bucket) {

	if bucket != nil {
		return bucket
	}

	b, err := couchbase.GetBucket("http://localhost:8091/", "default", "flowdle")
	if err != nil {
		log.Fatal("Cannot connect %s", err)
	}

	bucket = b
	return b
}
