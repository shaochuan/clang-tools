#!/bin/bash

git submodule init
git submodule update
CWD=$PWD
cd v8
git checkout master
cd "$CWD"
git submodule sync
git submodule foreach git pull

