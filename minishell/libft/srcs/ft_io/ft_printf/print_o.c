/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_o.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/02/09 19:52:41 by trponess          #+#    #+#             */
/*   Updated: 2018/03/28 18:35:03 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	width_o(int i, t_option *option)
{
	while (i < option->width)
	{
		if (option->zero && !option->minus && option->precision == -1)
			ft_stock_buf('0', ' ', ' ');
		else
			ft_stock_buf(' ', ' ', ' ');
		i++;
	}
}

void	add_width_o(t_option *option, int nb_len, const char *num)
{
	int i;
	int precision;
	int hash;

	if (option->precision < nb_len)
		precision = 0;
	else
		precision = option->precision - nb_len;
	if (!option->hash)
		hash = 0;
	else if ((option->hash && option->precision == -1) ||
			(option->precision <= nb_len && option->precision > -1))
		hash = 1;
	else
		hash = 0;
	if (num[0] == '0' && option->precision == 0)
		nb_len = 0;
	i = nb_len + precision + hash;
	width_o(i, option);
}

void	add_number_o(const char *num, t_option *option, int nb_len)
{
	int i;

	i = 0;
	if (option->hash && option->precision < nb_len)
		ft_stock_buf('0', '0', '0');
	if (num[0] == '-')
		nb_len -= 1;
	while (i < option->precision - nb_len)
	{
		ft_stock_buf('0', ' ', ' ');
		i++;
	}
	i = 0;
	if (num[0] == '0' && option->precision == 0)
		return ;
	if (num[0] == '-')
		i++;
	while (num[i])
	{
		ft_stock_buf(num[i], '0', '0');
		i++;
	}
}

char	*cast_nbo(t_option *option, long nb)
{
	char *num;

	if ((option->type == 'o') && (option->size == 'H'))
		num = ulong_to_str((unsigned char)nb, 8, option->type);
	else if ((option->type == 'o') && (option->size == 'h'))
		num = ulong_to_str((unsigned short int)nb, 8, option->type);
	else if ((option->type == 'o') && option->size == ' ')
		num = ulong_to_str((unsigned int)nb, 8, option->type);
	else if ((option->type == 'o') && (option->size == 'l'
			|| option->size == 'L'))
		num = ulong_to_str((unsigned long)nb, 8, option->type);
	else if (option->type == 'O')
		num = ulong_to_str((unsigned long)nb, 8, option->type);
	else if ((option->type == 'o') && (option->size == 'j'))
		num = ulong_to_str((uintmax_t)nb, 8, option->type);
	else if ((option->type == 'o') && (option->size == 'z'))
		num = ulong_to_str((int)nb, 8, option->type);
	else
		num = NULL;
	return (num);
}

int		print_o(t_option *option, va_list args)
{
	long	nb;
	int		nb_len;
	char	*num;

	nb = va_arg(args, long);
	num = cast_nbo(option, nb);
	nb_len = (int)ft_strlen(num);
	if (num[0] == '0' && option->hash)
	{
		ft_stock_buf('0', ' ', ' ');
		return (0);
	}
	if (!option->minus)
		add_width_o(option, nb_len, num);
	add_number_o(num, option, nb_len);
	if (option->minus)
		add_width_o(option, nb_len, num);
	;
	if ((int)ft_strlen(num) != 0)
		free(num);
	return (0);
}
