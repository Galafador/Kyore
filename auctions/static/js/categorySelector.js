    document.addEventListener('DOMContentLoaded', () => {
        //Gets all the elements
        const categorySelectorContainer = document.querySelector('.category-selector-container') 
        const dropdownHeader = document.getElementById('dropdownHeader')
        const dropdownContent = document.getElementById('dropdownContent')
        const dropdownArrow = document.getElementById('dropdownArrow')
        const selectedCategoryText = document.getElementById('selectedCategoryText')
        const selectedCategoryForm = document.getElementById('selectedCategoryForm')

        //Checks if a value already exists after first load
        if (selectedCategoryForm.value) {
            const categoryId = selectedCategoryForm.value
            fetch(`/get_category_breadcrumb?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {
                if (data.breadcrumb && data.breadcrumb.length > 0) {
                    const parts = []

                    data.breadcrumb.forEach((cat, index) => {
                        parts.push(`
                            <span class="breadcrumb-part">${cat.name}</span>
                        `)

                        if (index < data.breadcrumb.length -1) {
                            parts.push(`
                                <svg class="breadcrumb-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                                </svg>
                            `)
                        }
                    })

                    selectedCategoryText.innerHTML = parts.join('')
                }
            })
            .catch(err => {
                console.error("Failed to fetch breadcrumb: ", err)
            })
        }

        //Attach click listener to the header to open/close
        dropdownHeader.addEventListener('click', () => {
            toggleDropdown()
        })

        // Attach click listeners to all root category items
        const categoryItems = document.querySelectorAll(".category-item")
        categoryItems.forEach(item => {
            item.addEventListener('click', () => handleCategoryClick(item))
        })

        // Function to toggle open/close the category selector
        function toggleDropdown() {
            const isOpen = dropdownContent.classList.toggle('show')
            dropdownHeader.classList.toggle('closed', !isOpen)
            dropdownArrow.classList.toggle('rotate-180', isOpen)
            categorySelectorContainer.classList.toggle('opened', isOpen)
        }

        // function to update the text in the header with breadcrumb
        function updateSelectedCategoryText() {
            const selectedItems = document.querySelectorAll('.category-column .category-item.selected')
            
            // create a breadcrumb from selected items
            const parts = []
            selectedItems.forEach((item, index) => {
                const name = item.dataset.categoryName

                parts.push(`
                    <span class="breadcrumb-part">${name}</span>
                `)
    
                if (index < selectedItems.length - 1) {
                    parts.push(`
                        <svg class="breadcrumb-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                    `)
                }
            })
            selectedCategoryText.innerHTML = parts.join('')

            // update the value of a hidden form to POST
            if (selectedItems.length > 0) {
                const lastItem = selectedItems[selectedItems.length - 1]
                selectedCategoryForm.value = lastItem.dataset.categoryId
            } else {
                selectedCategoryForm.value = ""
            }
        }

        // function to handle when a category is clicked
        function handleCategoryClick(item) {
            const categoryId = item.dataset.categoryId
            const hasChildren = item.dataset.categoryHasChildren?.toLowerCase() === "true";

            const currentColumn = item.closest('.category-column')
            
            const siblings = currentColumn.querySelectorAll(".category-item")
            siblings.forEach(sibling => sibling.classList.remove('selected'))

            item.classList.add('selected')

            // Remove all columns after the current one
            while (currentColumn.nextElementSibling) {
                currentColumn.nextElementSibling.remove()
            }

            updateSelectedCategoryText()

            if (hasChildren) {
                fetch(`/get_child_categories?parent_id=${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.child_categories && data.child_categories.length > 0) {
                        const newColumn = document.createElement('div')
                        newColumn.classList.add('category-column')

                        const list = document.createElement('div')
                        list.classList.add('category-list')

                        data.child_categories.forEach(cat => {
                            const item = document.createElement('div')
                            item.classList.add('category-item', 'rounded')
                            item.dataset.categoryId = cat.id
                            item.dataset.categoryName = cat.name
                            let itemHasChildren = cat.has_children
                            item.dataset.categoryHasChildren = cat.has_children

                            const span = document.createElement('span')
                            span.classList.add('user-select-none')
                            span.textContent = cat.name

                            item.appendChild(span)
                            if (itemHasChildren) {
                                //add arrow icon
                                const arrow = `
                                <svg class="arrow-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                                </svg>
                                `
                                item.insertAdjacentHTML('beforeend', arrow);
                            }
                            
                            //add event listener to the item recursively
                            item.addEventListener('click', () => handleCategoryClick(item))
                            list.appendChild(item)
                        })

                        //append to the newly created column
                        newColumn.appendChild(list)
                        dropdownContent.appendChild(newColumn)

                        //automatically scroll to the right
                        dropdownContent.scrollLeft = dropdownContent.scrollWidth;
                    }
                })
                .catch(err => {
                    console.error("Failed to fetch categories: ", err)
                })
            }
            else {
                // automatically closes the dropdown when user clicks leaf category
                toggleDropdown()
            }
        }
    })