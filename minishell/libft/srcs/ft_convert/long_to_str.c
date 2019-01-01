/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   long_to_str.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/02/09 19:49:05 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*long_min(void)
{
	char *s;

	s = NULL;
	s = ft_strcpy(s, "-9223372036854775808");
	return (s);
}

char	*long_to_str(long value, int base, char cap)
{
	char	*s;
	long	n;
	int		sign;
	int		i;

	if (value == INTMAX_MIN)
		return (long_min());
	n = (value < 0) ? -value : value;
	sign = (value < 0 && base == 10) ? -1 : 0;
	i = (sign == -1) ? 2 : 1;
	while ((n /= base) >= 1)
		i++;
	s = (char*)malloc(sizeof(char) * (i + 1));
	s[i] = '\0';
	n = (value < 0) ? -value : value;
	while (i-- + sign)
	{
		if (ft_iscap(cap) == 1)
			s[i] = (n % base < 10) ? n % base + '0' : n % base + 'A' - 10;
		else
			s[i] = (n % base < 10) ? n % base + '0' : n % base + 'a' - 10;
		n /= base;
	}
	(i == 0) ? s[i] = '-' : 0;
	return (s);
}
