# Vulnerable Flask Web App

## Overview
Simple Flask web app that can be solved by using scanning tools to find available APIs.
Go to the relevant APIs to find clues on how to get the flag. There are numerous routes
that lead to nowhere, which will slow participants down.


### Flag
[[CyberWarrior_2022]]

## Steps to solve

1. Scan the site and determine the API's available to look at
2. Find the /user API and add a name. Can be actual username or made up name
3. You will see encryption keys from what looks to be a DB. Copy these keys and move on.
4. Find the /hello API and navigate there. Find to encrypt and decrypt commands. Copy the hashed text at the bottom.
5. Use one of the keys from step 3 to decrypt the flag.

*Flag Encryption:*<br/>
`echo [[CyberWarrior_2022]] | openssl aes-256-cbc -a -salt -pass pass:NotSureIfCoolEncryptionKey`

*Decryption*<br/>
`echo U2FsdGVkX18V/yyuJHUwDXcKayEkCmR0fA+kdi+YR29/nCauaFUAtyEqBanCDpAe | openssl aes-256-cbc -d -a -pass pass:NotSureIfCoolEncryptionKey`
