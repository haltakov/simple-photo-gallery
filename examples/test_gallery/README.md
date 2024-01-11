# Developer Gallery for Testing

This area is used to help with testing and not intended for end users. The
test gallery has 3 images from Library of Congress "free to use" maritime
collection and are believed to be unencumbered. The images came from here:

https://www.loc.gov/free-to-use/maritime-life/

They are relatively small file size to avoid adding large binaries to the repo.
Over time more photos may be added as additional test cases.

## Test overview

There is a Makefile to help with performing tests in a repeatable way. See
comments in the Makefile for more details about how to use it. It provides
targets for init-ing, building, and uploading the gallery in different ways.
The Makefile has a help target with some brief help:

    make help

## Special setups

Running basic init and build from files does not require any special setup.
But usein AWS or Netlify for uploads, and Google or Onedrive for albums
requires special setups:

### AWS S3

SPG supports uploading a gallery to AWS S3 as a static web site.
This is a brief high-level overview for testing with AWS. It is not a tutorial
about how to set up AWS and it can be a little complicated.

First, you need an AWS account. Then you have to create an S3 bucket.

Create AWS S3 account https://aws.amazon.com/s3/

Incomplete and not very detailed steps to set up s3:

Create a bucket. Configure it to serve static web site (properties)

You need to create a user that can access the bucket using the aws command
line tool. I could not get the IAM Identity Center to work for setting up a
user and giving permissions. So I gave up and used the deprecated IAM to create
a user.

Once I had the user, added policy in my bucket that looks like this:

```
{
    "Version": "2012-10-17",
    "Id": "Policy1704226183223",
    "Statement": [
        {
            "Sid": "Stmt1704226177122",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::xxxxxxxxx:user/Joe"
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::spg-gallery-test/*"
        },
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::spg-gallery-test/*"
        }
    ]
}
```

I also had to turn off all the "block public access" settings.

You need to install the aws command line tool and configure it. I did this with

   aws configure

and used my access key and secret key from my IAM user. After that you can try

   aws s3 ls

and you should see the name of your bucket

Once I did this, then `gallery-upload aws s3://spg-gallery-test` worked.
I was able to view the gallery at my bucket private URL.

### Netlify

SPG supports uploading a gallery to Netlify for a photos web site.

I have not yet got a test working for netlify at the time of this writing.

### Google Photos

SPG support building a photo gallery from photos in a google photo album.

To test this simply create a small album in google photos and then get the
album sharing URL. That URL can then be used for testing SPG gallery-init
with a google album.

### OneDrive Photos

At the time of this writing I have not tested with OneDrive.

