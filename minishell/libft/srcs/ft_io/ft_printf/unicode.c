/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   unicode.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/19 17:05:45 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:20:47 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

int		wchar_len(wchar_t ch)
{
	if (ch < (1 << 7))
		return (1);
	else if (ch < (1 << 11))
		return (2);
	else if (ch < (1 << 16))
		return (3);
	else if (ch < (1 << 21))
		return (4);
	else
		return (-1);
}

int		stru_len(wchar_t *str)
{
	int len_total;
	int len;
	int i;

	len = 0;
	len_total = 0;
	i = 0;
	while (str[i])
	{
		if ((len = wchar_len(str[i])) == -1)
			return (-1);
		len_total += len;
		i++;
	}
	return (len_total);
}

void	print_wchar(wchar_t ch)
{
	if (ch < (1 << 7))
		ft_stock_buf((unsigned char)ch, 0, 0);
	else if (ch < (1 << 11))
	{
		ft_stock_buf((unsigned char)(192 + (ch >> 6)), 0, 0);
		ft_stock_buf((unsigned char)(128 + (ch & 63)), 0, 0);
	}
	else if (ch < (1 << 16))
	{
		ft_stock_buf((unsigned char)(224 + (ch >> 12)), 0, 0);
		ft_stock_buf((unsigned char)(128 + ((ch >> 6) & 63)), 0, 0);
		ft_stock_buf((unsigned char)(128 + (ch & 63)), 0, 0);
	}
	else if (ch < (1 << 21))
	{
		ft_stock_buf((unsigned char)(240 + (ch >> 18)), 0, 0);
		ft_stock_buf((unsigned char)(128 + ((ch >> 12) & 63)), 0, 0);
		ft_stock_buf((unsigned char)(128 + ((ch >> 6) & 63)), 0, 0);
		ft_stock_buf((unsigned char)(128 + (ch & 63)), 0, 0);
	}
}

int		print_unicode_c(t_option *option, va_list args)
{
	wchar_t ch;
	int		len;

	ch = va_arg(args, wchar_t);
	if ((len = wchar_len(ch)) == -1)
		return (-1);
	if (!option->minus)
		add_widths(option, len);
	print_wchar(ch);
	if (option->minus)
		add_widths(option, len);
	return (0);
}

int		print_unicode_s(t_option *option, va_list args)
{
	wchar_t		*str;
	int			len;
	int			i;

	if ((str = va_arg(args, wchar_t *)) == NULL)
	{
		len = 6;
		if (!option->minus)
			add_widths(option, len);
		add_string(option, "(null)");
		if (option->minus)
			add_widths(option, len);
		return (0);
	}
	if ((len = stru_len(str)) == -1)
		return (-1);
	if (!option->minus)
		add_widths(option, len);
	i = -1;
	while (str[++i])
		print_wchar(str[i]);
	if (option->minus)
		add_widths(option, len);
	return (1);
}
