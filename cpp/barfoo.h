#pragma once
#include "bar.h"
#include "foo.h"
#include "third.h"
#include "inherit.h"

class barfoo : public bar, private third, public inherit <foo>
{
public:
	void barfoo_sing() {  };
};

