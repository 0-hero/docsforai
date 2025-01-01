# Documentation
Version: N/A
Author: Andreas M. Antonopoulos and Gavin Wood

---

## Table of Contents

### Gitbook Config

- [atlas.json](#atlasjson)

### Gitbook

- [LICENSE](#licensemd)
- [README](#readmemd)
- [CONTRIBUTING](#contributingmd)
- [code/jsonrpc/websockets/README](#code/jsonrpc/websockets/readmemd)
- [code/jsonrpc/http/js/README](#code/jsonrpc/http/js/readmemd)
- [code/auction dapp/README](#code/auction_dapp/readmemd)
- [code/auction dapp/DEV README](#code/auction_dapp/dev_readmemd)
- [code/auction dapp/frontend/README](#code/auction_dapp/frontend/readmemd)

### Gitbook Readme

- [README](#readmemd)


---

# Gitbook Config Documentation

## atlas.json

{
  "branch": "master",
  "files": [
    "cover.html",
    "praise.html",
    "titlepage.html",
    "copyright.html",
    "toc.html",
    "preface.asciidoc",
    "glossary.asciidoc",
    "01what-is.asciidoc",
    "02intro.asciidoc",
    "03clients.asciidoc",
    "04keys-addresses.asciidoc",
    "05wallets.asciidoc",
    "06transactions.asciidoc",
    "07smart-contracts-solidity.asciidoc",
    "08smart-contracts-vyper.asciidoc",
    "09smart-contracts-security.asciidoc",
    "10tokens.asciidoc",
    "11oracles.asciidoc",
    "12dapps.asciidoc",
    "13evm.asciidoc",
    "14consensus.asciidoc",
    "appdx-forks-history.asciidoc",
    "appdx-standards-eip-erc.asciidoc",
    "appdx-evm-opcodes-gas.asciidoc",
    "appdx-dev-tools.asciidoc",
    "appdx-web3js-tutorial.asciidoc",
    "appdx-shortlinks.asciidoc",
    "ix.html",
    "author_bio.html",
    "colo.html"
  ],
  "formats": {
    "pdf": {
      "version": "web",
      "toc": true,
      "index": true,
      "syntaxhighlighting": true,
      "show_comments": false,
      "antennahouse_version": "AHFormatterV62_64-MR4",
      "color_count": "1",
      "trim_size": "7inx9.1875in"
    },
    "epub": {
      "toc": true,
      "index": true,
      "syntaxhighlighting": true,
      "epubcheck": true,
      "show_comments": false,
      "downsample_images": true,
      "mathmlreplacement": false
    },
    "mobi": {
      "toc": true,
      "index": true,
      "syntaxhighlighting": true,
      "show_comments": false,
      "downsample_images": false
    },
    "html": {
      "toc": true,
      "index": true,
      "syntaxhighlighting": true,
      "show_comments": false,
      "consolidated": true
    }
  },
  "theme": "oreillymedia/animal_theme_sass",
  "title": "Mastering Ethereum",
  "templating": true,
  "print_isbn13": "9781491971949",
  "lang": "en",
  "accent_color": "cmyk(12%, 100%, 92%, 3%)"
}

---

# Gitbook Documentation

## LICENSE.md

# CC-BY-SA

## Creative Commons Attribution-ShareAlike 4.0

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">Mastering Ethereum</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://ethereumbook.info" property="cc:attributionName" rel="cc:attributionURL">Andreas M. Antonopoulos, Gavin Wood</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/ethereumbook/ethereumbook" rel="dct:source">https://github.com/ethereumbook/ethereumbook</a>.


---

## README.md

# Mastering Ethereum

![Mastering Ethereum Cover](images/cover_thumb.png)

Mastering Ethereum is a book for developers, offering a guide to the operation and use of the Ethereum, Ethereum Classic, RootStock (RSK) and other compatible EVM-based open blockchains.

## Reading this book

To read this book, see [book.asciidoc](https://github.com/ethereumbook/ethereumbook/blob/develop/book.asciidoc). Click on each of the chapters to read in your browser. Other parties may choose to release PDFs of the book online.

## Chapters
+ Preface: '[Preface](https://github.com/ethereumbook/ethereumbook/blob/develop/preface.asciidoc)'
+ Chapter 1: '[What Is Ethereum](https://github.com/ethereumbook/ethereumbook/blob/develop/01what-is.asciidoc)'
+ Chapter 2: '[Ethereum Basics](https://github.com/ethereumbook/ethereumbook/blob/develop/02intro.asciidoc)'
+ Chapter 3: '[Ethereum Clients](https://github.com/ethereumbook/ethereumbook/blob/develop/03clients.asciidoc)'
+ Chapter 4: '[Cryptography](https://github.com/ethereumbook/ethereumbook/blob/develop/04keys-addresses.asciidoc)'
+ Chapter 5: '[Wallets](https://github.com/ethereumbook/ethereumbook/blob/develop/05wallets.asciidoc)'
+ Chapter 6: '[Transactions](https://github.com/ethereumbook/ethereumbook/blob/develop/06transactions.asciidoc)'
+ Chapter 7: '[Smart Contracts and Solidity](https://github.com/ethereumbook/ethereumbook/blob/develop/07smart-contracts-solidity.asciidoc)'
+ Chapter 8: '[Smart Contracts and Vyper](https://github.com/ethereumbook/ethereumbook/blob/develop/08smart-contracts-vyper.asciidoc)'
+ Chapter 9: '[Smart Contract Security](https://github.com/ethereumbook/ethereumbook/blob/develop/09smart-contracts-security.asciidoc)'
+ Chapter 10: '[Tokens](https://github.com/ethereumbook/ethereumbook/blob/develop/10tokens.asciidoc)'
+ Chapter 11: '[Oracles](https://github.com/ethereumbook/ethereumbook/blob/develop/11oracles.asciidoc)'
+ Chapter 12: '[Decentralized Applications (DApps)](https://github.com/ethereumbook/ethereumbook/blob/develop/12dapps.asciidoc)'
+ Chapter 13: '[The Ethereum Virtual Machine](https://github.com/ethereumbook/ethereumbook/blob/develop/13evm.asciidoc)'
+ Chapter 14: '[Consensus](https://github.com/ethereumbook/ethereumbook/blob/develop/14consensus.asciidoc)'

## Content

The content status is "COMPLETE". The first edition of this book was published on December 1st, 2018. That edition is available in print and ebook format at many popular bookstores. It is tagged ["first_edition_first_print"](https://github.com/ethereumbook/ethereumbook/tree/first_edition_first_print) in the develop branch of this repository.

At this time, **only bug fix requests are accepted**. If you find a bug, start an issue or better yet, fix the problem with a pull request. We will start work on the second edition in late 2019.

## Source and license

The [first edition](https://github.com/ethereumbook/ethereumbook/tree/first_edition_first_print) of this book, as printed and sold by O'Reilly Media, is available in this repository.

Mastering Ethereum is released under the *Creative Commons CC-BY-SA license*.

This "Free Culture" compliant license was approved by our publisher O'Reilly Media (http://oreilly.com), who understands the value of open source. O'Reilly Media is not just the world's best publisher of technical books, but is also a strong supporter of this open culture and the sharing of knowledge.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">Mastering Ethereum</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://ethereumbook.info" property="cc:attributionName" rel="cc:attributionURL">Andreas M. Antonopoulos, Gavin Wood</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/ethereumbook/ethereumbook" rel="dct:source">https://github.com/ethereumbook/ethereumbook</a>.

# Translate This Book!

If you are interested in translating this book, please join our team of volunteers at: https://www.transifex.com/aantonop/ethereumbook


---

## CONTRIBUTING.md

# Guide to contributing

[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/ethereumbook/Lobby)

This book is developed collaboratively and openly, here on GitHub. We accept comments, contributions and corrections from all.

## Current Project STATUS
**CONTENT FREEZE - FIRST EDITION IN PRODUCTION**

## Contributing with a Pull Request

Before contributing with a Pull Request, please read the current **PROJECT STATUS**.

If the current **PROJECT STATUS** is **CONTENT FREEZE**, please keep these points in mind;

* Please submit only PRs for errors that a non-domain-expert copy editor might miss. Do not submit PRs for typos, grammar and syntax, as those are part of the copy editors job.
* Please don't merge code. Any changes will have to be applied manually (by the Author) after copy edit and before final proof, if the copy editor doesn't catch the same errors.


## Chat with the authors

You can chat with the authors and editors on [Gitter chat](https://gitter.im/ethereumbook/Lobby).

## License and attribution

All contributions must be properly licensed and attributed. If you are contributing your own original work, then you are offering it under a CC-BY license (Creative Commons Attribution). You are responsible for adding your own name or pseudonym in the Acknowledgments section in the [Preface](preface.asciidoc), as attribution for your contribution.

If you are sourcing a contribution from somewhere else, it must carry a compatible license. The book will initially be released under a CC-BY-NC-ND license which means that contributions must be licensed under open licenses such as MIT, CC0, CC-BY, etc. You need to indicate the original source and original license, by including an asciidoc markup comment above your contribution, like this:

```asciidoc
////
Source: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20-token-standard.md
License: CC0
Added by: @aantonop
////
```

The best way to contribute to this book is by making a pull request:

1. Login with your GitHub account or create one now
2. [Fork](https://github.com/ethereumbook/ethereumbook#fork-destination-box) the `ethereumbook` repository. Work on your fork.
3. Create a new branch on which to make your change, e.g. `git checkout -b my_code_contribution`, or make the change on the `develop` branch.
4. Please do one pull request PER asciidoc file, to avoid large merges. Edit the asciidoc file where you want to make a change or create a new asciidoc file in the `contrib` directory if you're not sure where your contribution might fit.
5. Edit `preface.asciidoc` and add your own name to the list of contributors under the Acknowledgment section. Use your name, or a GitHub username, or a pseudonym.
6. Commit your change. Include a commit message describing the correction.
7. Submit a pull request against the ethereumbook repository.

Here's a video tutorial to help you make your first pull request:

[![Ethereum Book Pull Request Tutorial](https://img.youtube.com/vi/IBYHohWm_5w/0.jpg)](https://www.youtube.com/watch?v=IBYHohWm_5w)

## Contributing with an issue

If you find a mistake and you're not sure how to fix it, or you don't know how to do a pull request, then you can file an Issue. Filing an Issue will help us see the problem and fix it.

Create a [new Issue](https://github.com/ethereumbook/ethereumbook/issues/new) now!

## Heading styles normalization across the book

Adjust heading style in each section as follows:

1. Only the chapter/section should be level 2, everything else should be level 3 and below (level 1 is the book title itself). Each asciidoc file should start with a "==" heading.
2. All lower case, except for first letter, proper nouns and acronyms. "What is this thing?", "What is the Ethereum sprocket?" "Who created the Ethereum Name Service (ENS)"
3. Acronyms are spelled out, capitalized, with the acronym in parentheses. Once you have spelled out an acronym in one heading, we can keep it as an acronym in subsequent headings.
4. No period at the end. Question mark if it is a question (generally avoid question headings, unless really appropriate)
5. Should include a unique anchor (see #279), all lower case, underscore separated.
6. Headings should be followed by a blank line.
7. Heading should be followed by a paragraph of text, not a lower-level heading without any text. If you find one like this, add a TODO comment (line of 4 slashes "////", line with "TODO: add paragraph", line of 4 slashes)

## Line endings

All submission should use Unix-like line endings: LF (not CR, not CR/LF). All the postprocessing is done on Unix-like systems. Incorrect line endings, or changes to line endings cause confusion for the diff tools and make the whole file look like it has changed.

If you are unsure or your OS makes things difficult, consider using a developer's text editor such as Atom.

## Thanks

We are very grateful for the support of the entire Ethereum community. With your help, this will be a great book that can help thousands of developers get started and eventually "master" Ethereum. Thank you!


---

## code/jsonrpc/websockets/README.md

# Ethereum WS Client

Connect to a node using Websockets and call the following rpc:
- Get accounts associated with a node(Only you should be able to access these endpoint)
- Get the current block number


## Build Setup

``` bash
# install dependencies
npm install

# run the node script
npm run rpc

```


---

## code/jsonrpc/http/js/README.md

# Ethereum HTTP Client

Connect to a node using HTTP(POST) and call the following rpc:
- Get accounts associated with a node(Only you should be able to access these endpoint)
- Get the current block number


## Build Setup

``` bash
# install dependencies
npm install

# run the node script
npm run http

```


---

## code/auction_dapp/README.md

# Decentralized Auction Application on Ethereum

This project aims to implement basic functionalities of an auction platform using Ethereum.

## Requirements

![Auction Diagram](auction_diagram.png)

The application should be decentralized and utilize Ethereum's stack:

1. Smart contracts for business logic(auctions, bids, refund and transfer of ownership)
2. Swarm for data storage(image and metadata)
3. Whisper for a peer-to-peer messaging(chatrooms)

### Deed Repository
Manage non-fungible tokens by implementing an asset/token/deed repository which holds unique asset/token/deed.

#### ERC: Non-fungible Token Standard #721 (NFT)
See following link: 
https://github.com/ethereum/eips/issues/721

### Auction Repository

Auction repository MUST act as an auction house which does the following:

- Holds asset/token/deed that is to be auctioned(ERC721 Ownership by smart contract)
- Allows users bid on auctions
- Keeps track of auctions/bids/ownership
- Transfers ownership of asset/token/deed to winder
- Transfers Funds to auction creator if auction is ended and there is at least one winner
- Cancels auction and deal with refunds
- UI to interact with the above functionality

### Front-end: Vuejs2.x + Vuetify

The front-end is developed using a reactive UI framework with integration of Vuetify, a Google's Material Design implementation.

## Implementation/Data flow

#### 1. Register an ERC721 Non-Fungible Token with the AuctionDaap Deed Repository

The idea of a Deed Repository is used across this project to hold any NFT with metadata attached to. A token/deed is registered by giving a unique ID and attaching metadata(TokenURI). The metadata is what makes each token important or valuable.

#### 2. Transfer Ownership of the NFT to AuctionRepository(Auction house)

The Auction house needs to verify that a NFT is owned by the auction creator, therefore before the auction is created, the owner should transfer the ownership of the NFT to the AuctionRepository smart contract address.

#### 3. Create Auction for NFT

Creating the auction is a simple process of entering auction details such as name, starting price, expiry date etc. The important part is to have the reference between the deed and the auction.

#### 4. Bid on Auction

Anyone can bid on an auction except the owner of the auction. Biding means that previous bidders are refunded and new bid is placed. Bid requirements are as follow:
1. Auction not expired
2. Bidder is not auction owner
3. Bid amount is greator than current bid or starting price(if no bid)

#### 5. Refunds

If an auction is canceled, the Auction Repository MUST return the ownership of the asset/token/deed back to the auction creator and refund bidders if any.

#### 6. Bidder Win Auction

If there is an auction winner, the asset/token/deed is transferred to the bidder and the bid amount is sent to the auction creator.



---

## code/auction_dapp/DEV_README.md

# Configuring truffle
Guide to properly configure truffle to build and deploy contracts to the network


## Add local testnet

Edit `truffle.js` :

```
  networks: {
    development: {
      host: "",
      port: 8545,
      network_id: "*",
      gas: 2900000
    }
  }
```

## Commands

```
$ truffle init #initialize truffle project
$ truffle console
$ truffle deploy
$ truffle migrate --reset --compile-all #redeploy the smat contracts

```

## Errors
Here is a list of possible errors:

## ParserError: Expected token Semicolon got 'LParen'

Emitting events gives compilation error if solc-js not 0.4.21
Update truffle using:

```
$ cd /usr/lib/node_modules/truffle
$ npm install solc@0.4.21 --save
```

### Account is locked/Auth needed

```
$ truffle console
truffle(development)> var acc = web3.eth.accounts[0]
truffle(development)> web3.personal.unlockAccount(acc, 'pass', 36000)
```

Then deploy. Repeat the step when needed

### Intrinsic gas too low

```
$ truffle console
truffle(development)> web3.eth.getBlock("pending").gasLimit
xxxxxxx
```

edit truffle.js

```
    development: {
        ...
        gas: xxxxxxxxx,
        network_id: "*"
    }
```


---

## code/auction_dapp/frontend/README.md

# Auction Platform Fronten

> Decentralized Auction Platform

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```



---

# Gitbook Readme Documentation

## README.md

# Mastering Ethereum

![Mastering Ethereum Cover](images/cover_thumb.png)

Mastering Ethereum is a book for developers, offering a guide to the operation and use of the Ethereum, Ethereum Classic, RootStock (RSK) and other compatible EVM-based open blockchains.

## Reading this book

To read this book, see [book.asciidoc](https://github.com/ethereumbook/ethereumbook/blob/develop/book.asciidoc). Click on each of the chapters to read in your browser. Other parties may choose to release PDFs of the book online.

## Chapters
+ Preface: '[Preface](https://github.com/ethereumbook/ethereumbook/blob/develop/preface.asciidoc)'
+ Chapter 1: '[What Is Ethereum](https://github.com/ethereumbook/ethereumbook/blob/develop/01what-is.asciidoc)'
+ Chapter 2: '[Ethereum Basics](https://github.com/ethereumbook/ethereumbook/blob/develop/02intro.asciidoc)'
+ Chapter 3: '[Ethereum Clients](https://github.com/ethereumbook/ethereumbook/blob/develop/03clients.asciidoc)'
+ Chapter 4: '[Cryptography](https://github.com/ethereumbook/ethereumbook/blob/develop/04keys-addresses.asciidoc)'
+ Chapter 5: '[Wallets](https://github.com/ethereumbook/ethereumbook/blob/develop/05wallets.asciidoc)'
+ Chapter 6: '[Transactions](https://github.com/ethereumbook/ethereumbook/blob/develop/06transactions.asciidoc)'
+ Chapter 7: '[Smart Contracts and Solidity](https://github.com/ethereumbook/ethereumbook/blob/develop/07smart-contracts-solidity.asciidoc)'
+ Chapter 8: '[Smart Contracts and Vyper](https://github.com/ethereumbook/ethereumbook/blob/develop/08smart-contracts-vyper.asciidoc)'
+ Chapter 9: '[Smart Contract Security](https://github.com/ethereumbook/ethereumbook/blob/develop/09smart-contracts-security.asciidoc)'
+ Chapter 10: '[Tokens](https://github.com/ethereumbook/ethereumbook/blob/develop/10tokens.asciidoc)'
+ Chapter 11: '[Oracles](https://github.com/ethereumbook/ethereumbook/blob/develop/11oracles.asciidoc)'
+ Chapter 12: '[Decentralized Applications (DApps)](https://github.com/ethereumbook/ethereumbook/blob/develop/12dapps.asciidoc)'
+ Chapter 13: '[The Ethereum Virtual Machine](https://github.com/ethereumbook/ethereumbook/blob/develop/13evm.asciidoc)'
+ Chapter 14: '[Consensus](https://github.com/ethereumbook/ethereumbook/blob/develop/14consensus.asciidoc)'

## Content

The content status is "COMPLETE". The first edition of this book was published on December 1st, 2018. That edition is available in print and ebook format at many popular bookstores. It is tagged ["first_edition_first_print"](https://github.com/ethereumbook/ethereumbook/tree/first_edition_first_print) in the develop branch of this repository.

At this time, **only bug fix requests are accepted**. If you find a bug, start an issue or better yet, fix the problem with a pull request. We will start work on the second edition in late 2019.

## Source and license

The [first edition](https://github.com/ethereumbook/ethereumbook/tree/first_edition_first_print) of this book, as printed and sold by O'Reilly Media, is available in this repository.

Mastering Ethereum is released under the *Creative Commons CC-BY-SA license*.

This "Free Culture" compliant license was approved by our publisher O'Reilly Media (http://oreilly.com), who understands the value of open source. O'Reilly Media is not just the world's best publisher of technical books, but is also a strong supporter of this open culture and the sharing of knowledge.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">Mastering Ethereum</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://ethereumbook.info" property="cc:attributionName" rel="cc:attributionURL">Andreas M. Antonopoulos, Gavin Wood</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/ethereumbook/ethereumbook" rel="dct:source">https://github.com/ethereumbook/ethereumbook</a>.

# Translate This Book!

If you are interested in translating this book, please join our team of volunteers at: https://www.transifex.com/aantonop/ethereumbook


---

