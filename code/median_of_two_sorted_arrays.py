class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        # Ensure nums1 is the shorter array for efficiency
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        x, y = len(nums1), len(nums2)
        low, high = 0, x
        
        while low <= high:
            partitionX = (low + high) // 2
            partitionY = (x + y + 1) // 2 - partitionX
            
            # If partitionX is 0, there is no element on the left side of X
            # Use -inf for maxX
            maxX = float('-inf') if partitionX == 0 else nums1[partitionX - 1]
            
            # If partitionX is len(nums1), there is no element on the right side of X
            # Use inf for minX
            minX = float('inf') if partitionX == x else nums1[partitionX]
            
            # Similar for Y
            maxY = float('-inf') if partitionY == 0 else nums2[partitionY - 1]
            minY = float('inf') if partitionY == y else nums2[partitionY]
            
            if maxX <= minY and maxY <= minX:
                # Found the correct partition
                # If total length is odd
                if (x + y) % 2 != 0:
                    return max(maxX, maxY)
                else:
                    return (max(maxX, maxY) + min(minX, minY)) / 2.0
            elif maxX > minY:
                # Move partition of X to the left
                high = partitionX - 1
            else:
                # Move partition of X to the right
                low = partitionX + 1
        
        # If we reach here, the input arrays were not sorted
        raise ValueError("Input arrays are not sorted") 