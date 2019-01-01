/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/23 18:27:17 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 19:01:21 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static t_list	*ft_lstadde(t_list *alst, t_list *new)
{
	if (alst->next)
		ft_lstadde(alst->next, new);
	else
		alst->next = new;
	return (alst);
}

t_list			*ft_lstmap(t_list *lst, t_list *(*f)(t_list *elem))
{
	t_list	*tmp;

	tmp = NULL;
	if (!lst)
		return (NULL);
	tmp = f(lst);
	if (!tmp || !f)
		return (NULL);
	return (ft_lstadde(tmp, ft_lstmap(lst->next, f)));
}
