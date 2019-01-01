/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lst_add.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/01/16 19:48:16 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	lst_add(t_list **list)
{
	t_list *elem;

	elem = (t_list *)malloc(sizeof(t_list));
	if (!elem)
		return ;
	if (!(*list))
		*list = lst_create_elem();
	else
	{
		while ((*list)->next)
			*list = (*list)->next;
		elem = lst_create_elem();
		elem->last = (*list);
		(*list)->next = elem;
		*list = (*list)->next;
	}
}
