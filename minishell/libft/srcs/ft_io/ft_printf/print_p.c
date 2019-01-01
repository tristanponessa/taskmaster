/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_p.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/08 20:21:05 by trponess          #+#    #+#             */
/*   Updated: 2018/03/27 17:12:16 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	ft_hash_p(void)
{
	ft_stock_buf('0', '0', '0');
	ft_stock_buf('x', '0', '0');
}

char	*cast_nbp(t_option *option, long *adress)
{
	char *num;

	if (option->type == 'p')
		num = ulong_to_str(*adress, 16, 's');
	else
		num = NULL;
	return (num);
}

void	print_p(t_option *option, va_list args)
{
	long	nb;
	int		nb_len;
	char	*num;
	long	*adress;

	nb = 0;
	adress = NULL;
	nb = va_arg(args, long);
	adress = (long *)&nb;
	num = cast_nbp(option, adress);
	option->hash = 1;
	option->plus = 0;
	option->space = 0;
	nb_len = (int)ft_strlen(num);
	if (option->zero)
		ft_hash_p();
	if (!option->minus)
		add_width_x(option, nb_len, num);
	if (!option->zero)
		ft_hash_p();
	add_number_x(num, option, nb_len);
	if (option->minus)
		add_width_x(option, nb_len, num);
	;
	free(num);
}
