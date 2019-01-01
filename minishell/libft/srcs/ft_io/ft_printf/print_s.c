/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_s.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/10 20:31:53 by trponess          #+#    #+#             */
/*   Updated: 2018/03/27 17:12:16 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	add_widths(t_option *option, int nb_len)
{
	int i;

	if (option->precision > -1 && nb_len > option->precision)
		nb_len = option->precision;
	i = nb_len;
	while (i < option->width)
	{
		if (option->zero)
			ft_stock_buf('0', ' ', ' ');
		else
			ft_stock_buf(' ', ' ', ' ');
		i++;
	}
}

void	add_string(t_option *option, const char *num)
{
	int i;

	i = 0;
	while (num[i] && (option->precision == -1 ||
		(i < option->precision && option->precision > -1)))
	{
		ft_stock_buf(num[i], '0', '0');
		i++;
	}
}

int		print_s(t_option *option, va_list args)
{
	char	*str;
	int		nb_len;

	str = NULL;
	str = va_arg(args, char *);
	if (str == NULL)
		str = "(null)";
	nb_len = (int)ft_strlen(str);
	if (!option->minus)
		add_widths(option, nb_len);
	add_string(option, str);
	if (option->minus)
		add_widths(option, nb_len);
	return (0);
}
