import numpy as np
import open3d as o3d


class PointCloudRemoval:

    def display_inlier_outlier(cloud, ind):
        # In Open3D tutorial they use select_down_sample, but this doesn't excist.
        # The correct function is: select_by_index
        inlier_cloud = cloud.select_by_index(ind)
        outlier_cloud = cloud.select_by_index(ind, invert=True)

        print("Showing outliers (red) and inliers (gray): ")
        outlier_cloud.paint_uniform_color([1, 0, 0])
        inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
        o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

    if __name__ == "__main__":
        print("Load a ply point cloud, print it, and render it")
        # pcd = o3d.io.read_point_cloud("../pointCloud_appel_boom/Apple/Apple view 1.xyz")
        pcd = o3d.io.read_point_cloud("D:/PEARTREE/Desktop_files/dot3dscan.ply")
        # ../pointCloud_appel_boom/Apple/Apple view 1.xyz
        # ../pointCloud/peerThijs.xyz
        print(pcd)
        print(np.asarray(pcd.points))
        o3d.visualization.draw_geometries([pcd])

        # print("Downsample the point cloud with a voxel of 0.02")
        voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.002)
        o3d.visualization.draw_geometries([voxel_down_pcd])

        print("Every 5th points are selected")
        uni_down_pcd = pcd.uniform_down_sample(every_k_points=5)
        o3d.visualization.draw_geometries([uni_down_pcd])

        print("Statistical oulier removal")
        # statistical_outlier_removal removes points that are further away from their
        # neighbors compared to the average for the point cloud. It takes two input parameters:

        # nb_neighbors allows to specify how many neighbors are taken into account
        # in order to calculate the average distance for a given point.

        # std_ratio allows to set the threshold level based on the standard deviation
        # of the average distances across the point cloud.
        # The lower this number the more aggressive the filter will be.
        cl, ind = uni_down_pcd.remove_statistical_outlier(nb_neighbors=20,
                                                          std_ratio=2.0)
        display_inlier_outlier(uni_down_pcd, ind)

        print("Radius oulier removal")
        # radius_outlier_removal removes points that have few neighbors in a given sphere around them.
        # Two parameters can be used to tune the filter to your data:

        # nb_points lets you pick the minimum amount of points that the sphere should contain

        # radius defines the radius of the sphere that will be used for counting the neighbors.
        # cl, ind = voxel_down_pcd.remove_radius_outlier(nb_points=8, radius=0.05)
        # display_inlier_outlier(voxel_down_pcd, ind)
        o3d.visualization.draw_geometries([cl])

        o3d.io.write_point_cloud("test.xyz", cl)
