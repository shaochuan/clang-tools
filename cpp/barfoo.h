#pragma once
#include "bar.h"
#include "foo.h"
#include "third.h"
class barfoo : public bar, public foo, private third
{
	void barfoo_sing();
};

