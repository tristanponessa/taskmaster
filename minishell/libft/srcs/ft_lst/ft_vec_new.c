/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_vec_new.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/04/04 18:11:26 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

t_vector	*ft_vec_new(void)
{
	t_vector *vec;

	vec = (t_vector *)malloc(sizeof(t_vector));
	vec->arr = ft_arrnew(VECTOR_SIZE);
	vec->len = 0;
	vec->cap = VECTOR_SIZE;
	return (vec);
}
