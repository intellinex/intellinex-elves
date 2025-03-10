# Elves Command:

### 1. Create new Model
```bash
source .venv/bin/activate
elves create-model model-name
```

# Pagination

```html
<span style="font-size: 13px;" >Showing Page {{ page }} of {{ (total + limit - 1) // limit }}</span>
                        

                        <!-- <div class="pagination">
                            {% if page > 1 %}
                            <a href="{{ url_for('list_location') }}?page={{ page - 1 }}&limit={{ limit }}">Previous</a>
                            {% endif %}
                            <span>Page {{ page }} of {{ (total + limit - 1) // limit }}</span>
                            {% if page * limit < total %}
                            <a href="{{ url_for('list_location') }}?page={{ page + 1 }}&limit={{ limit }}">Next</a>
                            {% endif %}
                        </div> -->

                        <div class="pagination">
                            {# Previous Button #}
                            {% if page <= 1 %}
                                <a href="#" aria-disabled="true" class="previous disabled">Previous</a>
                            {% else %}
                                <a href="{{ url_for('list_location') }}?page={{ page - 1 }}&limit={{ limit }}"
                                class="previous">
                                    Previous
                                </a>
                            {% endif %}
                        
                            {# Page Numbers #}
                            {% set total_pages = (total + limit - 1) // limit %}
                            {% if total_pages <= 5 %}
                                {# Show all pages if there are 5 or fewer pages #}
                                {% for p in range(1, total_pages + 1) %}
                                    {% if p == page %}
                                        <span class="current-page">{{ p }}</span>
                                    {% else %}
                                        <a href="{{ url_for('list_location') }}?page={{ p }}&limit={{ limit }}" class="pagination-button">{{ p }}</a>
                                    {% endif %}
                                {% endfor %}
                            {% else %}
                                {# Show first 2 pages, then [...] if current page is > 3, then current page and surrounding pages, then [...] if current page is < total_pages - 2, then last 2 pages #}
                                {% for p in range(1, 3) %}
                                    {% if p == page %}
                                        <span class="current-page">{{ p }}</span>
                                    {% else %}
                                        <a href="{{ url_for('list_location') }}?page={{ p }}&limit={{ limit }}" class="pagination-button">{{ p }}</a>
                                    {% endif %}
                                {% endfor %}
                        
                                {% if page > 3 %}
                                    <a href="#" class="pagination-button" >•••</a>
                                {% endif %}
                        
                                {% for p in range([page - 1, 3]|max, [page + 2, total_pages - 1]|min + 1) %}
                                    {% if p == page %}
                                        <span class="current-page">{{ p }}</span>
                                    {% else %}
                                        <a href="{{ url_for('list_location') }}?page={{ p }}&limit={{ limit }}" class="pagination-button">{{ p }}</a>
                                    {% endif %}
                                {% endfor %}
                        
                                {% if page < total_pages - 2 %}
                                        <a href="#" class="pagination-button" >•••</a>
                                {% endif %}
                        
                                {% for p in range(total_pages - 1, total_pages + 1) %}
                                    {% if p == page %}
                                        <span class="current-page">{{ p }}</span>
                                    {% else %}
                                        <a href="{{ url_for('list_location') }}?page={{ p }}&limit={{ limit }}" class="pagination-button">{{ p }}</a>
                                    {% endif %}
                                {% endfor %}
                            {% endif %}
                        
                            {# Next Button #}
                            {% if page * limit >= total %}
                                <a href="#" aria-disabled="false" class="next">Next</a>
                            {% else %}
                                <a href="{{ url_for('list_location') }}?page={{ page + 1 }}&limit={{ limit }}" class="next">Next</a>
                            {% endif %}
                        
                        </div>
```