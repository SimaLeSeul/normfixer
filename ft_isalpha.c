#include "libft.h"

int ft_isalpha(int c)
{
	int	a;
	int	b;

	a = 0;
	b = 0;
	if ((c >= 65 && c <= 90) || (c >= 97 && c <= 122))
		return (c);
	return (0);
}
