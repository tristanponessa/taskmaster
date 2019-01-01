/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   elem_set_value.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/01/16 19:47:46 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	elem_set_value(t_list **list, int n, char c, char mod)
{
	if (mod == 'c')
		(*list)->ch = c;
	if (mod == 'n')
		(*list)->nb = n;
	if (mod == 'a')
	{
		(*list)->ch = c;
		(*list)->nb = n;
	}
}
