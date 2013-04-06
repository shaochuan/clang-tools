#pragma once
#include "bar_specific.h"
#include "foo.h"
#include "third.h"
#include "inherit.h"

class barfoo : public bar_specific, private third, public inherit <foo>
{
public:
	void barfoo_sing() {  };
};

