/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   str_to_ulong.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/28 17:36:18 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int				ft_isblank(char c)
{
	if (c <= 32)
		return (1);
	return (0);
}

int				isvalid(char c, int base)
{
	char *digits;
	char *digits2;

	digits = ft_strdup("0123456789abcdef");
	digits2 = ft_strdup("0123456789ABCDEF");
	while (base--)
		if (digits[base] == c || digits2[base] == c)
		{
			free(digits);
			free(digits2);
			return (1);
		}
	free(digits);
	free(digits2);
	return (0);
}

int				value_of(char c)
{
	if (c >= '0' && c <= '9')
		return (c - '0');
	else if (c >= 'a' && c <= 'f')
		return (c - 'a' + 10);
	else if (c >= 'A' && c <= 'F')
		return (c - 'A' + 10);
	return (0);
}

unsigned long	str_to_ulong(const char *str, int str_base)
{
	unsigned long	result;
	int				sign;

	result = 0;
	while (ft_isblank(*str))
		str++;
	sign = 1;
	(*str == '+') ? ++str : 0;
	while (isvalid(*str, str_base))
		result = result * str_base + value_of(*str++);
	return (result * sign);
}
