from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def view_pagination(request, n_el, model_elem):
    """
    Function to use paginator in many views
    """
    paginator = Paginator(model_elem, n_el)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an int, deliver the first page.
        products = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return (products)


def page_indexing(elems, np_display):
    # Get the index of the current page
    index = elems.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = elems.paginator.num_pages
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - np_display if index >= np_display else 0
    end_index = (
        index + np_display if index <= max_index - np_display else max_index
    )
    # Get our new page range.
    # In the latest versions of Django page_range returns an iterator.
    # Thus pass it to list, to make our slice possible again.
    page_range = list(elems.paginator.page_range)[start_index:end_index]

    return page_range
