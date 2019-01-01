/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_do_op.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/30 08:29:38 by trponess          #+#    #+#             */
/*   Updated: 2018/04/04 19:28:27 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

intmax_t	ft_factorial(intmax_t a)
{
	int i;
	int res;
	int h;

	i = 0;
	res = 0;
	h = 0;
	while (i++ < a)
	{
		res = res + (a - h);
		h++;
	}
	return (res);
}

intmax_t	ft_power(intmax_t a, intmax_t b)
{
	int i;
	int res;

	i = 0;
	res = 1;
	while (i++ < b)
		res = res * a;
	return (res);
}

intmax_t	ft_do_op(intmax_t a, char sign, intmax_t b)
{
	if (sign == '+')
		return (a + b);
	if (sign == '-')
		return (a - b);
	if (sign == '*')
		return (a * b);
	if (sign == '/')
		return (a / b);
	if (sign == '%')
		return (a % b);
	if (sign == '!')
		return (ft_factorial(a));
	if (sign == '^')
		return (ft_power(a, b));
	if (sign == 'R')
		return (ft_sqrt(b));
	return (0);
}
