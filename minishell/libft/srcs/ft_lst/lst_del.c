/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lst_del.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/01/16 19:49:25 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	lst_del(t_list **list)
{
	if (!(*list))
		return ;
	while ((*list)->next)
		(*list) = (*list)->next;
	while ((*list)->last)
	{
		(*list) = (*list)->last;
		free((*list)->next);
		(*list)->next = NULL;
	}
	free((*list)->next);
	(*list)->next = NULL;
	free(*list);
	(*list) = NULL;
}
