"""H3C NETCONF XML Configuration Command Templates.

Interface Configuration Commands
"""

# Create ACL (acl number)
CREATE_ACL = """
<config>
	<top xmlns="http://www.h3c.com/netconf/config:1.0">
		<ACL>
			<Groups>
				<Group>
					<GroupType>1</GroupType>
					<GroupID>{acl_num}</GroupID>
 				</Group>
			</Groups>
		</ACL>	
	</top>
</config>
"""
