/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:10:46 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:02:54 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putstr(const char *str)
{
	int i;

	if (!str)
		return ((void)NULL);
	i = 0;
	while (str[i])
	{
		ft_putchar(str[i]);
		i++;
	}
}
