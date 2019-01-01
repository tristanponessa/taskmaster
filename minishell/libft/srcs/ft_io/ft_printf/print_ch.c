/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_ch.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/02/09 19:50:11 by trponess          #+#    #+#             */
/*   Updated: 2018/03/27 17:12:16 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

int		print_c(t_option *option, va_list args)
{
	char	ch;
	int		i;

	i = 1;
	ch = (char)va_arg(args, int);
	if (option->minus == 1)
		ft_stock_buf(ch, '0', '0');
	while (i < option->width)
	{
		if (option->zero)
			ft_stock_buf('0', '0', '0');
		else
			ft_stock_buf(' ', '0', '0');
		i++;
	}
	if (option->minus == 0)
		ft_stock_buf(ch, '0', '0');
	return (1);
}
