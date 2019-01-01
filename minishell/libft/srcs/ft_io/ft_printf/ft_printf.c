/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/01/23 17:52:15 by trponess          #+#    #+#             */
/*   Updated: 2018/09/22 18:22:04 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	print_else(t_option *option)
{
	int i;

	i = 0;
	while (i + 1 < option->width && !option->minus)
	{
		if (option->zero)
			ft_stock_buf('0', ' ', ' ');
		else
			ft_stock_buf(' ', ' ', ' ');
		i++;
	}
	ft_stock_buf(option->type, ' ', ' ');
	while (i + 1 < option->width && option->minus)
	{
		if (option->zero)
			ft_stock_buf('0', ' ', ' ');
		else
			ft_stock_buf(' ', ' ', ' ');
		i++;
	}
}

int		print_type(t_option *option, va_list args)
{
	if (option->type == 'u' || option->type == 'U')
		print_u(option, args);
	else if (option->type == 'd' || option->type == 'D' || option->type == 'i')
		print_d(option, args);
	else if (option->type == 'x' || option->type == 'X')
		print_x(option, args);
	else if (option->type == 'p')
		print_p(option, args);
	else if (option->type == 'o' || option->type == 'O')
		print_o(option, args);
	else if (option->type == 'c')
		print_c(option, args);
	else if (option->type == 's')
		print_s(option, args);
	else if (option->type == 'C')
		print_unicode_c(option, args);
	else if (option->type == 'S')
		print_unicode_s(option, args);
	else
		print_else(option);
	return (1);
}

int		check_if_valid(const char *str)
{
	int i;
	int save;

	i = 0;
	while (str[i] && str[i] != '%')
		i++;
	save = i;
	i++;
	while (str[i] && str[save] == '%')
	{
		if (ft_strchr("sSpdDioOuUxXcC%", str[i]))
			return (1);
		i++;
	}
	return (-1);
}

int		ft_printf(const char *str, ...)
{
	va_list		args;
	t_option	option;
	int			i;

	i = 0;
	catch_fd(1, 1);
	va_start(args, str);
	if (str == NULL)
		return (0);
	while (str[i])
	{
		if (str[i] == '%' && check_if_valid(str) == 1)
		{
			i++;
			check_stock_input(str, &i, &option);
			print_type(&option, args);
		}
		else if (str[i] != '%')
			ft_stock_buf(str[i], '0', '0');
		i++;
	}
	i = ft_stock_buf('\0', '0', 's');
	ft_stock_buf('\0', 'r', '0');
	va_end(args);
	return (i);
}

int		ft_fprintf(int fd, const char *str, ...)
{
	va_list		args;
	t_option	option;
	int			i;

	i = 0;
	catch_fd(fd, 1);
	va_start(args, str);
	if (str == NULL)
		return (0);
	while (str[i])
	{
		if (str[i] == '%' && check_if_valid(str) == 1)
		{
			i++;
			check_stock_input(str, &i, &option);
			print_type(&option, args);
		}
		else if (str[i] != '%')
			ft_stock_buf(str[i], '0', '0');
		i++;
	}
	i = ft_stock_buf('\0', '0', 's');
	ft_stock_buf('\0', 'r', '0');
	va_end(args);
	return (i);
}
