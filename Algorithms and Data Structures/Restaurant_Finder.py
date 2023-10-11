# Name: Sura Venkata Sri Anish
# Student ID: 32045980

# Question 1

def restaurantFinder(d, site_list):
    """
    Function description:
    This function finds the maximum possible revenue and the sites to visit to achieve this revenue. The function uses a dynamic programming approach to solve the problem.

    Approach description:
    The function iterates through the list of sites and for each site, it calculates the maximum revenue by either including or excluding the current site. It then backtracks to find the selected sites.

    :Input:
    d: The minimum distance between any two selected sites.
    site_list: A list of revenues for each site.

    :Output, return or postcondition:
    The function returns a tuple where the first element is the maximum possible revenue and the second element is a list of selected sites in ascending order.

    :Time complexity:
    O(n), where n is the number of sites.

    :Aux space complexity:
    O(n), where n is the number of sites.
    """
    n = len(site_list)

    # Initializing a list to store the maximum revenue for each site
    site_sum = [0] * (n + 1)

    # Initializing a list to store the selected sites
    selected_sites = []

    # Iterating through the sites
    for i in range(1, n + 1):
        
        # Calculating the maximum revenue without the current site
        skip_site_revenue = site_sum[i - 1]
        
        # Calculating the maximum revenue with the current site
        include_site_revenue = site_list[i - 1]
        if i - d - 1 >= 0:
            include_site_revenue += site_sum[i - d - 1]

        # Updating site_sum with the maximum revenue for the current site
        site_sum[i] = max(skip_site_revenue, include_site_revenue)

    # Backtracking to find the selected sites
    i = n
    while i > 0:
        
        # If the current site's revenue is not equal to the previous site's revenue, it means this site was selected
        if site_sum[i] != site_sum[i - 1]:
            selected_sites.append(i) 
            
            # Move to the site at least 'd' distance away
            i -= d + 1
        
        else:
            i -= 1

    # Reversing the selected_sites list to ensure it's in ascending order, since the sites are taken in descending order
    selected_sites.reverse()

    # Calculate the total revenue
    total_revenue = site_sum[-1]

    return total_revenue, selected_sites

d = 0
site_list = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
result = restaurantFinder(d, site_list)
print(result)